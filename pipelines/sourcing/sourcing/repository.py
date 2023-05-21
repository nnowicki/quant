from dagster import load_assets_from_package_module, repository

from sourcing import assets


@repository
def sourcing():
    return [load_assets_from_package_module(assets)]
