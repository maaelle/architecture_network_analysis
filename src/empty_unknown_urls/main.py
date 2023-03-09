from mongo import get_all_unknown_urls, delete_all_unknown_urls


def lambda_handler(event):
    unknown_urls = get_all_unknown_urls()
    delete_all_unknown_urls()


lambda_handler({})
