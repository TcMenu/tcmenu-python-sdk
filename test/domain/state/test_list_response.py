from tcmenu.domain.state.list_response import ListResponse


def test_list_response():
    lr = ListResponse(row=100, response_type=ListResponse.ResponseType.SELECT_ITEM)
    assert lr.response_type == ListResponse.ResponseType.SELECT_ITEM
    assert lr.row == 100
    assert str(lr) == "100:0"

    lr2 = ListResponse.from_string("202:1")
    assert lr2.response_type == ListResponse.ResponseType.INVOKE_ITEM
    assert lr2.row == 202
    assert str(lr2) == "202:1"

    assert ListResponse.from_string("sldkfghkjd:2") is None
    assert ListResponse.from_string("sldkfghkjd") is None
