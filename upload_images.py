#!/usr/bin/env python3
"""Batch upload all menu item images to the API."""
import subprocess, json, os

API = "http://localhost:5000"
IMG_BASE = "/home/ramo/Projects/retro-spot/Data/items_images"

IMAGE_MAP = {
    # Soft drinks
    "695d5eba-e627-448f-b9cd-93092670e891": f"{IMG_BASE}/soft_drinks/pepsi.jpeg",
    "3a02b67c-7886-43e4-83a6-9e81fbc32ca1": f"{IMG_BASE}/soft_drinks/sprite.jpeg",
    # Yogurt
    "f3109572-7a94-487e-8d8c-b06e64408861": f"{IMG_BASE}/yogurt/flavor_yogurt.jpeg",
    "6acd5b28-af81-45ea-959a-05fdb4fee677": f"{IMG_BASE}/yogurt/honey_yogurt.jpeg",
    # Ice Cream
    "abcddad4-14f0-42aa-8aea-73254f5f5cc2": f"{IMG_BASE}/ice_cream/2scoops.jpeg",
    "d8fe95fa-f078-4189-b278-b69185523bdb": f"{IMG_BASE}/ice_cream/3scoops.jpeg",
    "100ff8c3-5ceb-4ca3-9ff3-2f380c495bff": f"{IMG_BASE}/ice_cream/4scoops.jpeg",
    # Smoothie
    "2dcc603b-c592-4b91-9acb-4d54194008fd": f"{IMG_BASE}/smoothie/blueberry_smoothie.jpeg",
    "180c00db-70c5-4bba-8df2-6ead9d7b48ce": f"{IMG_BASE}/smoothie/kiwi_smoothie.jpeg",
    "21735693-b98b-45d9-9968-dbbca20e4b31": f"{IMG_BASE}/smoothie/lemon_mint_smoothie.jpeg",
    "8e1b9598-0626-4051-a715-aa1fc3f3f1c4": f"{IMG_BASE}/smoothie/lemon_smoothie.jpeg",
    "90e027c4-de50-443e-b280-c9908429f73c": f"{IMG_BASE}/smoothie/mango_passion_fruit_smoothie.jpeg",
    "01aa7c8d-cc15-433c-8c4a-fdd00a60d167": f"{IMG_BASE}/smoothie/mango_smoothie.jpeg",
    "066d6086-c0e6-4f7a-942d-823e4162a5c7": f"{IMG_BASE}/smoothie/passion_fruit_smoothie.jpeg",
    "9ac148f7-b645-4db3-83d8-9f1f3b1456cc": f"{IMG_BASE}/smoothie/peach_smoothie.jpeg",
    "f3ba9198-a5d8-4f92-905a-93b021ecbd95": f"{IMG_BASE}/smoothie/raspberry_smoothie.jpeg",
    "49205953-a59e-4f50-8da2-b1b5d718f4ae": f"{IMG_BASE}/smoothie/strawberry_smoothie.jpeg",
    "b3355098-2089-4510-b80e-8d04eae2d9d2": f"{IMG_BASE}/smoothie/strawberry_watermelon_smoothie.jpeg",
    "2a3a53e6-189a-4c8b-9e2f-c24cb78ace9e": f"{IMG_BASE}/smoothie/watermelon_smoothie.jpeg",
    # Fresh Juice
    "59bc0b6b-44ab-4b14-8e5c-bd372a4ac366": f"{IMG_BASE}/juice/date_milk_juice.jpeg",
    "936d2123-3083-4163-9aca-58f6d8ab156f": f"{IMG_BASE}/juice/french_lemon_juice.jpeg",
    "25288dd1-704b-4768-9624-f94e92a2dc08": f"{IMG_BASE}/juice/guava_juice.jpeg",
    "955d6d08-65b5-45a9-a1b4-f2f4eaf52655": f"{IMG_BASE}/juice/guava_milk_juice.jpeg",
    "d2a52c01-9aba-4fb7-b9ec-1194fe1a597a": f"{IMG_BASE}/juice/kiwi_juice.jpeg",
    "b0fd3e7a-1a29-41ad-9a0b-07520a77945b": f"{IMG_BASE}/juice/lemon_juice.jpeg",
    "1b778c8d-9f04-432f-b07f-3af31ed07608": f"{IMG_BASE}/juice/lemon_mint_juice.jpeg",
    "d689f993-dcde-4cd6-a8fe-1a437f7a190f": f"{IMG_BASE}/juice/mango_juice.jpeg",
    "1f0deb6d-633d-4810-bcd1-f26da3e296c7": f"{IMG_BASE}/juice/orange_juice.jpeg",
    "8c863e85-6c56-4c4a-9643-d6a772f61880": f"{IMG_BASE}/juice/strawberry_juice.jpeg",
    "09fa5661-102f-432a-b63b-f794265c94b9": f"{IMG_BASE}/juice/strawberry_milk_juice.jpeg",
    "759273ea-f9b8-42e7-8005-6a5393ad5a90": f"{IMG_BASE}/juice/watermelon_juice.jpeg",
    # Frappe
    "1f68cb4b-3959-4f9d-a7de-afcd0ec557d6": f"{IMG_BASE}/frappe/frappe_caramel.jpeg",
    "3207714c-546e-4c72-91e5-92c40f62b0f5": f"{IMG_BASE}/frappe/frappe_lotus.jpeg",
    "05c064ef-2d1a-4ac7-9f39-0b05057063a7": f"{IMG_BASE}/frappe/frappe_mocha.jpeg",
    "3b302c18-a168-41ae-a066-fa03a9228585": f"{IMG_BASE}/frappe/frappe_notilla.jpeg",
    "34fcc847-3530-431c-ba14-eb0d6b817d6c": f"{IMG_BASE}/frappe/fappe_psitachio.jpeg",
    "74f54dbf-c5c6-4d34-987b-c86d67bba6e8": f"{IMG_BASE}/frappe/frappe_vanilla.jpeg",
    "aaafae57-0ae8-4dee-9c59-6b52d2961589": f"{IMG_BASE}/frappe/frappuccino_classic.jpeg",
    "5ca03fa8-e5da-457f-83b1-bb5c1c236c6f": f"{IMG_BASE}/frappe/frappuccino_flavor.jpeg",
    # Cocktails
    "755c0716-a83e-4e33-a705-6167552b0c83": f"{IMG_BASE}/cocktails/florida.jpeg",
    "4a832264-f202-4ac1-a638-ec89e96fa760": f"{IMG_BASE}/cocktails/froment.jpeg",
    "46b1a3d4-9e5c-4ec7-8668-e0af51626205": f"{IMG_BASE}/cocktails/lemus.jpeg",
    "71bae5d7-0852-4701-af0b-f030c0698609": f"{IMG_BASE}/cocktails/mango_energy.jpeg",
    "2d7c1eec-b256-4eff-834b-49f2d9e27cdc": f"{IMG_BASE}/cocktails/three_flowers.jpeg",
    # Tea and Herbs
    "a0114ee0-f44a-4bd5-a7db-a22f02f06b30": f"{IMG_BASE}/tea_herbs/anise.jpeg",
    "03502b4e-e18b-48de-99af-776af6b10245": f"{IMG_BASE}/tea_herbs/cinnamon_milk.jpeg",
    "736f6359-b6fb-4478-8262-c1bb9f4e3aed": f"{IMG_BASE}/tea_herbs/ginger.jpeg",
    "00159e79-3606-44f0-bb66-ef963921b3e4": f"{IMG_BASE}/tea_herbs/green_tea.jpeg",
    "e4ed6ebc-140c-4621-8815-cd4e7a3c0c2f": f"{IMG_BASE}/tea_herbs/herbla_mix.jpeg",
    "3009ae36-17ec-40ff-bddf-7e67f6ced2eb": f"{IMG_BASE}/tea_herbs/lemon.jpeg",
    "51d6a2b6-0596-428b-bbe1-5cd53cbcae01": f"{IMG_BASE}/tea_herbs/milk_tea.jpeg",
    "fa3fbc2d-6b6d-4571-a80b-264b72225564": f"{IMG_BASE}/tea_herbs/mint.jpeg",
    "be3910cc-f8d1-4df0-996d-d206e2a904ad": f"{IMG_BASE}/tea_herbs/tea.jpeg",
    # Waffle
    "abd5ce12-f5db-4c41-a233-9a036e6ca880": f"{IMG_BASE}/waffle/waffle_lotus.jpeg",
    "d1449bd3-9925-4b1a-b8e5-a781bbec7da2": f"{IMG_BASE}/waffle/waffle_nutella.jpeg",
    "1e7d3360-efb4-4242-8117-5eceb4a2d1bf": f"{IMG_BASE}/waffle/waffle_pistachio.jpeg",
    "028ede50-b3f5-4573-9a05-83e01a1256b8": f"{IMG_BASE}/waffle/waffle_mixed.jpeg",
    "9764ef1e-139a-4312-b1c4-924a0b971bdd": f"{IMG_BASE}/waffle/waffle_white_chocolate.jpeg",
}

success, failed = 0, 0

for item_id, img_path in IMAGE_MAP.items():
    if not os.path.exists(img_path):
        print(f"  MISSING: {img_path}")
        failed += 1
        continue

    result = subprocess.run([
        "curl", "-s", "-X", "PATCH",
        f"{API}/api/menu-items/{item_id}/details",
        "-F", f"image=@{img_path}",
    ], capture_output=True, text=True)

    try:
        resp = json.loads(result.stdout)
        if resp.get("imageUrl"):
            name = img_path.split("/")[-1]
            print(f"  ✓ {name} → {resp['imageUrl']}")
            success += 1
        else:
            print(f"  ✗ {item_id[:8]}... → {result.stdout[:120]}")
            failed += 1
    except Exception:
        print(f"  ✗ {item_id[:8]}... → {result.stdout[:120]}")
        failed += 1

print(f"\n{'='*40}")
print(f"Done: {success} uploaded, {failed} failed")
