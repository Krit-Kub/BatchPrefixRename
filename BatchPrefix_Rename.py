import unreal

# กำหนด class
Dev_name = "Biskrit"
target_folder = "/Game/ICRC_Box"

# ดึง ToolsHelpers and Library จาก UE
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

assets = unreal.EditorAssetLibrary.list_assets(target_folder, recursive=True)
total_assets = len(assets)

count_texture = 0
count_staticmesh = 0
count_material = 0
count_material_instance = 0

with unreal.ScopedSlowTask(total_assets, f"Renaming Assets in {target_folder}") as slow_task:
    slow_task.make_dialog(True)

    for asset_path in assets:
        asset = unreal.load_asset(asset_path)
        if asset is None:
            slow_task.enter_progress_frame(1)
            continue

        name = asset.get_name()
        renamed = False

        if isinstance(asset, unreal.Texture) and not name.startswith("TX_"):
            new_name = f"TX_{name}"
            renamed = True
            count_texture += 1
        elif isinstance(asset, unreal.StaticMesh) and not name.startswith("SM_"):
            new_name = f"SM_{name}"
            renamed = True
            count_staticmesh += 1
        elif isinstance(asset, unreal.Material) and not name.startswith("M_"):
            new_name = f"M_{name}"
            renamed = True
            count_material += 1
        elif isinstance(asset, unreal.MaterialInstance) and not name.startswith("MI_"):
            new_name = f"MI_{name}"
            renamed = True
            count_material_instance += 1

        if renamed:
            asset_tools.rename_assets([unreal.AssetRenameData(asset, asset.get_path_name().rpartition('/')[0], new_name)])
            print(f"[{Dev_name}] Renamed: {name} -> {new_name}")

        slow_task.enter_progress_frame(1)

# สรุป log
print("\n✅ Rename complete for folder:", target_folder)
print(f"[{Dev_name}] Summary:")
print(f"Textures renamed: {count_texture}")
print(f"StaticMeshes renamed: {count_staticmesh}")
print(f"Materials renamed: {count_material}")
print(f"Material Instances renamed: {count_material_instance}")
print(f"Developed by: {Dev_name}")

# -------------------------
# Pop-up message พร้อม summary
summary_message = (
    f"✅ All assets renamed successfully!\n\n"
    f"Textures: {count_texture}\n"
    f"StaticMeshes: {count_staticmesh}\n"
    f"Materials: {count_material}\n"
    f"Material Instances: {count_material_instance}\n\n"
    f"Developed by: {Dev_name}"
)

unreal.EditorDialog.show_message(
    title="Rename Complete",
    message=summary_message,
    message_type=unreal.AppMsgType.OK
)
