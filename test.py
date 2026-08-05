# import random
# from typing import Annotated
#
# from pydantic import AfterValidator
#
# data = {
#     "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
#     "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
#     "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
# }
#
# def check_valid_id(id: str):
#     if not id.startswith(("isbn-", "imdb-")):
#         raise ValueError("Invalid ID format, it must start with 'isbn-' or 'imdb-'")
#     return id
#
# def read_items_(q: Annotated[str|None, AfterValidator(check_valid_id)] = None):
#     if q:
#         item = data[q]
#         print(item)
#     else:
#         result = random.choice(list(data.items()))
#         print(result)
#
#     # return {"id": q, "item": item}

