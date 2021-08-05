import atexit

from concurrent import futures

import grpc

from koapy.backend.kiwoom_open_api_plus.grpc import KiwoomOpenApiPlusService_pb2_grpc
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceServicer import (
    KiwoomOpenApiPlusServiceServicer,
)
from koapy.config import config
from koapy.utils.logging.Logging import Logging
from koapy.utils.networking import find_free_port_for_host, is_in_private_network


class KiwoomOpenApiPlusServiceServer(Logging):
    def __init__(
        self,
        control,
        host=None,
        port=None,
        max_workers=None,
        credentials=None,
        **kwargs,
    ):
        if host is None:
            host = config.get_string(
                "koapy.backend.kiwoom_open_api_plus.grpc.host", "localhost"
            )
            host = config.get_string(
                "koapy.backend.kiwoom_open_api_plus.grpc.server.host", host
            )
        if port is None:
            port = config.get_int("koapy.backend.kiwoom_open_api_plus.grpc.port", 0)
            port = config.get_int(
                "koapy.backend.kiwoom_open_api_plus.grpc.server.port", port
            )

        if port == 0:
            port = find_free_port_for_host(host)
            self.logger.info(
                "Using one of the free ports, final address would be %s:%d", host, port
            )

        if max_workers is None:
            max_workers = config.get_int(
                "koapy.backend.kiwoom_open_api_plus.grpc.server.max_workers", 8
            )

        self._control = control
        self._host = host
        self._port = port
        self._max_workers = max_workers
        self._credentials = credentials
        self._kwargs = kwargs

        self._servicer = KiwoomOpenApiPlusServiceServicer(self._control)
        self._address = self._host + ":" + str(self._port)

        if "thread_pool" in self._kwargs:
            self._executor = self._kwargs.pop("thread_pool")
        else:
            self._executor = futures.ThreadPoolExecutor(max_workers=self._max_workers)

        self._server = None
        self._server_started = False
        self._server_stopped = False

        self.reinitialize_server()

        atexit.register(self._executor.shutdown, False)

    def __del__(self):
        atexit.unregister(self._executor.shutdown)

    def reinitialize_server(self):
        if self._server is not None:
            self.stop()
            self.wait_for_termination()

        self._server = grpc.server(self._executor, **self._kwargs)
        self._server_started = False
        self._server_stopped = False

        KiwoomOpenApiPlusService_pb2_grpc.add_KiwoomOpenApiPlusServiceServicer_to_server(
            self._servicer, self._server
        )

        if self._credentials is None:
            if not is_in_private_network(self._host):
                self.logger.warning(
                    "Adding insecure port %s to server, but the address is not private.",
                    self._address,
                )
            self._server.add_insecure_port(self._address)
        else:
            self._server.add_secure_port(self._address, self._credentials)

    def get_host(self):
        return self._host

    def get_port(self):
        return self._port

    def start(self):
        if self._server_started and self._server_stopped:
            self.reinitialize_server()
        if not self._server_started:
            self._server.start()
            self._server_started = True

    def wait_for_termination(self, timeout=None):
        return self._server.wait_for_termination(timeout)

    def is_running(self):
        return self.wait_for_termination(1)

    def stop(self, grace=None):
        event = self._server.stop(grace)
        self._server_stopped = True
        return event

    def __getattr__(self, name):
        return getattr(self._server, name)
