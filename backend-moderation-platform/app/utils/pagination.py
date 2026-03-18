from fastapi import Request

def get_pagination(request: Request):

    page = int(request.query_params.get("page", 1))
    limit = int(request.query_params.get("limit", 10))

    skip = (page - 1) * limit

    return {
        "page": page,
        "limit": limit,
        "skip": skip
    }


def paginate_query(query, pagination):

    total_records = query.order_by(None).count()
    results = query.offset(pagination["skip"]).limit(pagination["limit"]).all()

    total_pages = (total_records + pagination["limit"] - 1) // pagination["limit"]

    pagination_data = {
        "page":  pagination["page"],
        "limit": pagination["limit"],
        "total_records": total_records,
        "total_pages": total_pages
    }

    return results, pagination_data