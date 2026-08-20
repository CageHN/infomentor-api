from __future__ import annotations

from infomentor.api._base import HubResource
from infomentor.models import DocumentList, LinkList, NewsList


def communication_sort_key(sort: str = "desc", sort_by: str = "date") -> str:
    """Build the ``field___SORT_*`` keys used by Hub communication lists."""
    sort_word = {
        "asc": "SORT_ASC",
        "desc": "SORT_DESC",
        "none": "SORT_NONE",
    }.get(sort.lower(), "SORT_DESC")
    field = {
        "date": "lastPublishDate",
        "title": "title",
        "author": "publishedBy",
        "name": "title",
    }.get(sort_by.lower(), sort_by)
    return f"{field}___{sort_word}"


class CommunicationAPI(HubResource):
    def app_data(self) -> dict:
        return self.post("/communication/communication/appData") or {}

    def get_news_list(
        self,
        *,
        page_size: int = -1,
        sort: str = "desc",
        sort_by: str = "date",
    ) -> NewsList:
        data = (
            self.post(
                "/Communication/News/GetNewsList",
                json={"pageSize": page_size, "sortBy": communication_sort_key(sort, sort_by)},
            )
            or {}
        )
        if isinstance(data, list):
            data = {"items": data}
        return NewsList.model_validate(data)

    def get_documents_list(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
        sort: str = "desc",
        sort_by: str = "date",
        type_ids: list[int] | None = None,
    ) -> DocumentList:
        data = (
            self.post(
                "/Communication/Documents/GetDocumentsList",
                json={
                    "page": page,
                    "pageSize": page_size,
                    "sortBy": communication_sort_key(sort, sort_by),
                    "typeIds": ",".join(str(i) for i in type_ids) if type_ids else "",
                },
            )
            or {}
        )
        return DocumentList.model_validate(data)

    def get_links_list(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
        sort: str = "asc",
        sort_by: str = "title",
        type_ids: list[int] | None = None,
    ) -> LinkList:
        data = (
            self.post(
                "/Communication/Links/GetLinksList",
                json={
                    "page": page,
                    "pageSize": page_size,
                    "sortBy": communication_sort_key(sort, sort_by),
                    "typeIds": ",".join(str(i) for i in type_ids) if type_ids else "",
                },
            )
            or {}
        )
        return LinkList.model_validate(data)

    def get_consents(self) -> dict:
        return self.post("/Communication/Consents/GetCurrentList") or {}

    def get_article(self, news_id: int | str) -> dict:
        """Legacy IM1-style article endpoint used by m42e/infomentor."""
        return self.post("/News/news/GetArticle", json={"id": news_id}) or {}
