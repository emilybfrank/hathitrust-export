from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image
from os import makedirs, listdir
from os.path import isfile, join, exists, splitext
import fire

CHROMEDRIVER_PATH = '/Users/mleclimber/Desktop/chromedriver/chromedriver'
SAVE_PATH = '/Users/mleclimber/Desktop'
# can't go directly to the SSO login page. Need to be redirected.
SSO_INTRO_URL = 'https://bobcat.library.nyu.edu/primo-explore/search?query=any,contains,Art%20of%20the%20Past:%20Sources%20and%20Reconstruction:%20Proceedings%20of%20the%20First%20Symposium%20of%20the%20Art%20Technological%20Source%20Research%20Study%20Group&tab=all&search_scope=all&sortby=rank&vid=NYU&lang=en_US&mode=basic'

def check_for_auth():
  user_input = input('Press any key to continue, once logged in using the new chromedriver window.')

def check_for_completeness():
  user_input = input('Press any key to continue, once verified that all the pages successfully downloaded.')

def check_for_yes():
  user_input = input('Did that work? You can check and see if the chromedriver window successfully loaded any pages, and/or new files were saved to the book folder. If it did type "yes". Anything other than that will rerun the last step.')
  return user_input == 'yes'

def run(book_id, start, end):
    driver = auth()
    check_for_auth()

    try:
        driver = retrieve(driver, book_id, start, end)
    except:
        print('hit an error')

    # rerun until the user confirms it worked (it's flaky)
    while not check_for_yes():
        try:
            driver = retrieve(driver, book_id, start, end)
        except:
            print('hit an error')

    check_for_completeness()

    combine(book_id)
    quit(driver)


def auth():
    print('Opening chromedriver to authenticate with SSO')
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
    driver.get(SSO_INTRO_URL)
    wait = WebDriverWait(driver, 10)
    return driver


def retrieve(driver, book_id, start, end):
    """Function that retrieves page-by-page png files for a book id."""
    # book_id = 'mdp.39015025096234' # (an example)
    print('Retrieving pages {0} - {1} for doc {2}'.format(start, end, book_id))

    directory = join(SAVE_PATH, '{0}'.format(book_id))
    if not exists(directory):
        makedirs(directory)

    for page_num in range(int(start),int(end) + 1):
        page_url = 'https://babel.hathitrust.org/cgi/imgsrv/image?id={0};seq={1};size=250;rotation=0'.format(book_id, page_num)
        driver.get(page_url)
        wait = WebDriverWait(driver, 8)

        full_path = join(directory, 'page_{0}.png'.format(page_num))

        page_img = driver.find_element_by_tag_name('img')
        _save_image(driver, page_img, full_path)
        print('\tRetrieved page {0} ({1})'.format(page_num, full_path))

    return driver


def combine(book_id):
    print('Combining pages...')
    path = join(SAVE_PATH, '{0}'.format(book_id))
    files = [f for f in listdir(path) if isfile(join(path, f))]
    sorted_files = sorted(files,key=lambda x: int(splitext(x)[0].split("_")[1])) 

    # handle first image separately, then append others
    pil_image1 = Image.open(join(path,sorted_files[0]))                                         
    converted1 = pil_image1.convert('RGB')

    converted_img_list = []
    for img in sorted_files[1:]:
        pil_image = Image.open(join(path,img))                                         
        converted = pil_image.convert('RGB')
        converted_img_list.append(converted)  

    outfile_name = join(path, '{0}.pdf'.format(book_id))
    converted1.save(outfile_name, save_all=True, append_images=converted_img_list)

def quit(driver):
    print('Quitting session')
    driver.quit()

#################################
############ HELPERS ############
#################################
def _save_image(chrome, element, save_path):
    # in case the image isn't isn't in the view yet
    location = element.location_once_scrolled_into_view

    # saves screenshot of entire page
    chrome.save_screenshot(save_path)

    # crop after in memory, using PIL
    image = Image.open(save_path)
    width = 1000
    height = 1419
    left = 700
    bottom = height
    image = image.crop((left, 0, left + width, height)) 
    image.save(save_path, 'png')  # saves new cropped image

if __name__ == '__main__':
  fire.Fire()