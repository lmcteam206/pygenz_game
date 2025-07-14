from engine.asset_manager import SimpleAssetManager, resource_path

resources = SimpleAssetManager(
    pack_file=resource_path("game_assets.pack"),
    key=b"my_key",  # Same key you used in the packer
    encrypted=True,
)
