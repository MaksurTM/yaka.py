import os,pycurl,selenium,time,glob,sys,argparse
from selenium import webdriver

### Functions ###

def scrape_images(QUERY:str, MAX_LINKS:int, browser:webdriver, sleep_between_interactions:int=0.5):

    def scroll_to_end(browser):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

    # load page
    URL = ("https://duckduckgo.com/?q="+QUERY+"&t=h_&iar=images")
    browser.get(URL)
    time.sleep(5) # let it load
    image_urls = set()
    img_count = 0
    results_start = 0

    while img_count < MAX_LINKS:
        # finds the number of displayed results
        scroll_to_end(browser)
        thumbnail_results = browser.find_elements_by_css_selector(".tile--img__img") # tiled image selector
        number_results = len(thumbnail_results)
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        # Clicks the tiled images that were found and extracts the full res URL from each one
        for img in thumbnail_results[results_start:number_results]:
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue
            actual_images = browser.find_elements_by_css_selector('.detail__media__img-highres') # selected image selector

            for actual_image in actual_images:
                # gets the full res URL from the src attribute and adds to the list
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            # stops for loop if it exceeds the number of images requested
            img_count = len(image_urls)
            if len(image_urls) >= MAX_LINKS:
                print(f"Found: {len(image_urls)} image links, done!")
                break

        # move the result startpoint further down
        results_start = len(thumbnail_results)
    return image_urls
    print(image_urls)

# Uses cURL to save the images.
def download_image(folder_path:str,url:str,i:int):
    try:
        file_path = (folder_path+"/out"+str(i)+".jpg")
        with open(file_path, 'wb') as f:
            c = pycurl.Curl()
            c.setopt(c.URL, url)
            c.setopt(c.WRITEDATA, f)
            c.perform()
            c.close()
        print(f"SUCCESS - saved {file_path}")
    except Exception as ex:
        print(f"ERROR - Could not download {url} - {ex}")

# Function that makes use of previous two functions.
def search_and_download(search_term:str,target_path:str,number_images=5):
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    with webdriver.Firefox() as browser:
        hres = scrape_images(QUERY, MAX_LINKS, browser, 0.25)
    i = 0
    for elem in hres:
        download_image(target_path,elem,i)
        i += 1

# Creates images in img folder from downloaded images in images folder
def crop_images(output:str):
    if not os.path.exists(output):
        os.makedirs(output)
    os.system("magick mogrify -resize 1280x720\! -quality 100 -path img/ src/out*.jpg")
    print("Resized")

def make_video():
    # Removes previous iteration if existing.
    if os.path.exists("yaka.mp4"):
        os.remove("yaka.mp4")

    # Creates video from images in the images folder.
    os.system("ffmpeg -framerate 10/1 -pattern_type glob -i 'img/*.jpg' \
            -c:v libx264 -r 30 -pix_fmt yuv420p yaka0.mp4")

    # Adds the song.
    os.system("ffmpeg -i yaka0.mp4 -i audio.mp3 -map 0:v -map 1:a -c:v copy -shortest yaka.mp4")

def clean_up():
    os.remove("yaka0.mp4")
    os.remove("geckodriver.log")
    files = glob.glob('./img/*')
    for f in files:
        os.remove(f)
    files = glob.glob('./src/*')
    for f in files:
        os.remove(f)
    os.rmdir("./src")
    os.rmdir("./img")


### Main ###

# Argument Parsing
parser = argparse.ArgumentParser()

# -q QUERY -n MAXLINKS -c
parser.add_argument("QUERY", type=str, help="Target to download images of.")
parser.add_argument("-n", "--number", type=int, help="Number if images to download.")
parser.add_argument('-k', "--keep", action='store_true')
args = parser.parse_args()

print("Query: {}\nImage Number: {}\nKeep Files: {}\n".format(args.QUERY,args.number,args.keep))

#  Main variables
QUERY = args.QUERY
NO_CLEAN = args.keep
if args.number == None :
    MAX_LINKS = 698
else :
    MAX_LINKS = args.number

def main(QUERY:str,MAX_LINKS:int,NO_CLEAN:bool) :
    search_and_download(QUERY,"./src",MAX_LINKS)
    crop_images("img")
    make_video()
    if NO_CLEAN == False :
        clean_up()
    else :
        print("Keeping extra files.")
main(QUERY,MAX_LINKS,NO_CLEAN)
