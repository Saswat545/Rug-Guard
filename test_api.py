"""
TEST_API.PY — Run this before build_dataset.py
Usage: python test_api.py --api_key YOUR_KEY
Expected: ✅ ALL TESTS PASSED
"""
import sys, requests, argparse

def test_api(api_key):
    print("=" * 55)
    print("RugGuard — Etherscan V2 API Test")
    print("=" * 55)

    BASE = "https://api.etherscan.io/v2/api"

    # 1. Internet
    print("\n[1/4] Internet connection...")
    try:
        requests.get("https://api.etherscan.io", timeout=8)
        print("      ✅ Etherscan reachable")
    except Exception as e:
        print(f"      ❌ {e}"); sys.exit(1)

    # 2. API key with V2
    print("\n[2/4] API key validity (V2 endpoint)...")
    try:
        r = requests.get(BASE, params={
            "chainid": 1, "module": "stats",
            "action": "ethsupply", "apikey": api_key
        }, timeout=10)
        data = r.json()
        if data.get("status") == "1":
            print("      ✅ API key valid, V2 working")
        elif "Invalid API Key" in str(data.get("result", "")):
            print(f"      ❌ Invalid API key"); sys.exit(1)
        else:
            print(f"      ⚠️  Response: {data}")
    except Exception as e:
        print(f"      ❌ {e}"); sys.exit(1)

    # 3. Fetch known contract (WETH)
    print("\n[3/4] Fetching WETH source code...")
    WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    try:
        r = requests.get(BASE, params={
            "chainid": 1, "module": "contract",
            "action": "getsourcecode",
            "address": WETH, "apikey": api_key
        }, timeout=15)
        data = r.json()
        if data.get("status") == "1":
            src = data["result"][0].get("SourceCode", "")
            name = data["result"][0].get("ContractName", "?")
            print(f"      ✅ Fetched {name} ({len(src):,} chars)")
        else:
            print(f"      ❌ {data.get('message')} — {data.get('result')}"); sys.exit(1)
    except Exception as e:
        print(f"      ❌ {e}"); sys.exit(1)

    # 4. Feature extraction
    print("\n[4/4] Feature extraction...")
    try:
        from backend.feature_extractor import extract_features
        feats = extract_features(src)
        print(f"      ✅ {len(feats)} features extracted")
    except Exception as e:
        print(f"      ❌ {e}"); sys.exit(1)

    print()
    print("=" * 55)
    print("✅ ALL TESTS PASSED — run build_dataset.py now")
    print("=" * 55)
    print(f"\n  python build_dataset.py --api_key {api_key}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--api_key", required=True)
    test_api(p.parse_args().api_key)