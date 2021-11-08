from up9lib import *
from authentication import authenticate

# logging.basicConfig(level=logging.DEBUG)


@data_driven_tests
class Tests_www_pousadaportela_com_br(unittest.TestCase):

    @clear_session({'spanId': 1})
    def test_01_get_(self):
        # GET https://www.pousadaportela.com.br/ (endp 1)
        www_pousadaportela_com_br = get_http_client('https://www.pousadaportela.com.br', authenticate)
        resp = www_pousadaportela_com_br.get('/')
        resp.assert_ok()
        # resp.assert_status_code(200)
        # resp.assert_cssselect('section.mbr-fullscreen div.align-center.container div.row.justify-content-center div h1.mbr-section-title.mbr-fonts-style.mbr-white strong', expected_value='Venha nos visitar UAI !!!')
        # resp.assert_cssselect('html head title', expected_value='Pousada Portela')
        # self.assertLess(resp.elapsed.total_seconds(), 0.690)
