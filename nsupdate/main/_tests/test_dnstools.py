"""
Tests for dnstools module.
"""

import pytest

from ..dnstools import (query_ns, parse_name, update_ns,
                        BASEDOMAIN, NONEXISTING_HOST,
                        WWW_HOST, WWW_IPV4_HOST, WWW_IPV4_IP, WWW_IPV6_HOST, WWW_IPV6_IP, )

from dns.resolver import NXDOMAIN


class TestQuery(object):
    def test_queries_ok(self):
        assert query_ns(WWW_IPV4_HOST, 'A') == WWW_IPV4_IP  # v4 ONLY
        assert query_ns(WWW_IPV6_HOST, 'AAAA') == WWW_IPV6_IP  # v6 ONLY
        assert query_ns(WWW_HOST, 'A') == WWW_IPV4_IP  # v4 and v6, query v4
        assert query_ns(WWW_HOST, 'AAAA') == WWW_IPV6_IP  # v4 and v6, query v6

    def test_queries_failing(self):
        with pytest.raises(NXDOMAIN):
            query_ns(NONEXISTING_HOST, 'A')
        with pytest.raises(NXDOMAIN):
            query_ns(NONEXISTING_HOST, 'AAAA')


class TestUpdate(object):
    def test_parse1(self):
        origin, relname = parse_name('foo.' + BASEDOMAIN)
        assert str(origin) == BASEDOMAIN + '.'
        assert str(relname) == 'foo'

    def test_parse2(self):
        origin, relname = parse_name('foo.bar.' + BASEDOMAIN)
        assert str(origin) == BASEDOMAIN + '.'
        assert str(relname) == 'foo.bar'

    def test_parse_with_origin(self):
        origin, relname = parse_name('foo.bar.baz.org', 'bar.baz.org')
        assert str(origin) == 'bar.baz.org' + '.'
        assert str(relname) == 'foo'

    def test_add_del_v4(self):
        host, ip = 'test1.' + BASEDOMAIN, '1.1.1.1'
        response = update_ns(host, 'A', ip, action='add', ttl=60)
        print response
        assert query_ns(host, 'A') == ip
        response = update_ns(host, 'A', action='del')
        print response
        with pytest.raises(NXDOMAIN):
            query_ns(host, 'A') == ip

    def test_update_v4(self):
        host, ip = 'test2.' + BASEDOMAIN, '2.2.2.2'
        response = update_ns(host, 'A', ip, action='upd', ttl=60)
        print response
        assert query_ns(host, 'A') == ip

        host, ip = 'test2.' + BASEDOMAIN, '3.3.3.3'
        response = update_ns(host, 'A', ip, action='upd', ttl=60)
        print response
        assert query_ns(host, 'A') == ip

    def test_add_del_v6(self):
        host, ip = 'test3.' + BASEDOMAIN, '::1'
        response = update_ns(host, 'AAAA', ip, action='add', ttl=60)
        print response
        assert query_ns(host, 'AAAA') == ip
        response = update_ns(host, 'AAAA', action='del')
        print response
        with pytest.raises(NXDOMAIN):
            query_ns(host, 'AAAA') == ip

    def test_update_v6(self):
        host, ip = 'test4.' + BASEDOMAIN, '::2'
        response = update_ns(host, 'AAAA', ip, action='upd', ttl=60)
        print response
        assert query_ns(host, 'AAAA') == ip

        host, ip = 'test4.' + BASEDOMAIN, '::3'
        response = update_ns(host, 'AAAA', ip, action='upd', ttl=60)
        print response
        assert query_ns(host, 'AAAA') == ip

    def test_update_mixed(self):
        host4, ip4 = 'test5.' + BASEDOMAIN, '4.4.4.4'
        response = update_ns(host4, 'A', ip4, action='upd', ttl=60)
        print response
        assert query_ns(host4, 'A') == ip4

        host6, ip6 = 'test5.' + BASEDOMAIN, '::4'
        response = update_ns(host6, 'AAAA', ip6, action='upd', ttl=60)
        print response
        assert query_ns(host6, 'AAAA') == ip6

        # make sure the v4 is unchanged
        assert query_ns(host4, 'A') == ip4

        host4, ip4 = 'test5.' + BASEDOMAIN, '5.5.5.5'
        response = update_ns(host4, 'A', ip4, action='upd', ttl=60)
        print response
        assert query_ns(host4, 'A') == ip4

        # make sure the v6 is unchanged
        assert query_ns(host6, 'AAAA') == ip6
