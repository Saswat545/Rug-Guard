"""
LEGIT_CONTRACTS.PY
==================
Curated list of verified legitimate Ethereum smart contracts.
These are the NEGATIVE class (label=0) for RugGuard's ML model.

Sources:
- Uniswap official deployments
- Aave V2/V3 protocol contracts
- Compound Finance
- Chainlink price feeds
- Standard OpenZeppelin ERC-20 tokens (verified, long-running)
- MakerDAO
- Curve Finance

All contracts:
  - Verified source code on Etherscan
  - Active for 1+ years with no exploit history
  - Open source and audited
"""

LEGIT_ADDRESSES = [
    # ── Uniswap V2 ──────────────────────────────────────────────
    "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6",  # UniswapV2Factory
    "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488",  # UniswapV2Router02
    "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc",  # USDC/ETH Pair
    "0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852",  # ETH/USDT Pair
    "0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11",  # DAI/ETH Pair
    "0xBb2b8038a1640196FbE3e38816F3e67Cba72D940",  # WBTC/ETH Pair
    "0xf80758aB42C3B07dA84053Fd88804bCB6BAA4b5",  # SHIB/ETH Pair

    # ── Uniswap V3 ──────────────────────────────────────────────
    "0x1F98431c8aD98523631AE4a59f267346ea31F984",  # UniswapV3Factory
    "0xE592427A0AEce92De3Edee1F18E0157C05861564",  # SwapRouter
    "0xC36442b4a4522E871399CD717aBDD847Ab11FE88",  # NonfungiblePositionManager
    "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",  # USDC/ETH 0.05% pool
    "0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8",  # USDC/ETH 0.3% pool
    "0x4e68Ccd3E89f51C3074ca5072bbAC773960dFa36",  # ETH/USDT 0.3% pool

    # ── Aave V2 ─────────────────────────────────────────────────
    "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9",  # LendingPool
    "0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5",  # LendingPoolAddressesProvider
    "0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d",  # IncentivesController
    "0xd784927Ff2f95ba542BfC824c8a8a98F3495f6b5",  # StakedAave

    # ── Aave V3 ─────────────────────────────────────────────────
    "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2",  # Pool V3
    "0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e",  # PoolAddressesProvider

    # ── Compound ────────────────────────────────────────────────
    "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3b",  # Comptroller
    "0xc00e94Cb662C3520282E6f5717214004A7f26888",  # COMP token
    "0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5",  # cETH
    "0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643",  # cDAI
    "0x39AA39c021dfbaE8faC545936693aC917d5E7563",  # cUSDC

    # ── MakerDAO ────────────────────────────────────────────────
    "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2",  # MKR token
    "0x6B175474E89094C44Da98b954EedeAC495271d0F",  # DAI token
    "0x35D1b3F3D7966A1DFe207aa4514C12a259A0492B",  # MCD_VAT
    "0x19c0976f590D67707E62397C87829d896Dc0f1F",   # MCD_JUG

    # ── Chainlink ───────────────────────────────────────────────
    "0x514910771AF9Ca656af840dff83E8264EcF986CA",  # LINK token
    "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419",  # ETH/USD Price Feed
    "0x2c1d072e956AFFC0D435Cb7AC308d97B35A9b8e",   # LINK/USD Price Feed
    "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88b",  # BTC/USD Price Feed
    "0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6",  # USDC/USD Price Feed

    # ── WETH & stablecoins ──────────────────────────────────────
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC
    "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT
    "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",  # WBTC
    "0x4Fabb145d64652a948d72533023f6E7A623C7C53",  # BUSD (Paxos)
    "0x8E870D67F660D95d5be530380D0eC0bd388289E1",  # USDP

    # ── Curve Finance ───────────────────────────────────────────
    "0xD533a949740bb3306d119CC777fa900bA034cd52",  # CRV token
    "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7",  # 3pool (DAI/USDC/USDT)
    "0xA5407eAE9Ba41422680e2e00537571bcC53efBfD",  # sUSD pool
    "0xDeBF20617708857ebe4F679508E7b7863a8A8EeE",  # aDAI/aUSDC/aUSDT

    # ── Lido ────────────────────────────────────────────────────
    "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",  # stETH
    "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32",  # LDO token

    # ── Balancer ────────────────────────────────────────────────
    "0xba100000625a3754423978a60c9317c58a424e3D",  # BAL token
    "0xBA12222222228d8Ba445958a75a0704d566BF2C8",  # Vault

    # ── OpenZeppelin standard ERC-20s (verified, long-running) ──
    "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",  # UNI token
    "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9",  # AAVE token
    "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e",  # YFI token
    "0xc944E90C64B2c07662A292be6244BDf05Cda44a7",  # GRT token
    "0x4a220E6096B25EADb88358cb44068A3248254675",  # QNT token
    "0xD31a59c85aE9D8edEFeC411D448f90841571b89c",  # SOL (wrapped)
    "0x6810e776880C02933D47DB1b9fc05908e5386b96",  # GNO token
    "0x111111111117dC0aa78b770fA6A738034120C302",  # 1INCH token
    "0xC18360217D8F7Ab5e7c516566761Ea12Ce7F9D72",  # ENS token
    "0xBB0E17EF65F82Ab018d8EDd776e8DD940327B28b",  # AXS token

    # ── ENS ─────────────────────────────────────────────────────
    "0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85",  # ENS NFT
    "0x253553366Da8546fC250F225fe3d25d0C782303b",  # ENS RegistrarController

    # ── Gnosis Safe ─────────────────────────────────────────────
    "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",  # GnosisSafe L1
    "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",  # GnosisSafe L2

    # ── OpenSea ─────────────────────────────────────────────────
    "0x00000000006c3852cbEf3e08E8dF289169EdE581",  # Seaport 1.1
    "0x0000000000000068F116a894984e2DB1123eB395",  # Seaport 1.6

    # ── Convex Finance ──────────────────────────────────────────
    "0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B",  # CVX token
    "0xF403C135812408BFbE8713b5A23a04b3D48AAE31",  # Booster

    # ── Rocket Pool ─────────────────────────────────────────────
    "0xD33526068D116cE69F19A9ee46F0bd304F21A51f",  # RPL token
    "0xae78736Cd615f374D3085123A210448E74Fc6393",  # rETH

    # ── Frax ────────────────────────────────────────────────────
    "0x853d955aCEf822Db058eb8505911ED77F175b99e",  # FRAX
    "0x3432B6A60D23Ca0dFCa7761B7ab56459D9C964D0",  # FXS

    # ── dYdX ────────────────────────────────────────────────────
    "0x92D6C1e31e14520e676a687F0a93788B716BEff5",  # DYDX token

    # ── Synthetix ───────────────────────────────────────────────
    "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6f",  # SNX token
    "0x57Ab1ec28D129707052df4dF418D58a2D46d5f51",  # sUSD

    # ── The Graph ───────────────────────────────────────────────
    "0xc944E90C64B2c07662A292be6244BDf05Cda44a7",  # GRT

    # ── Additional verified ERC-20s ─────────────────────────────
    "0x6DEA81C8171D0bA574754EF6F8b412F2Ed88c54D",  # LQTY
    "0x5f98805A4E8be255a32880FDeC7F6728C6568bA0",  # LUSD
    "0xEB4C2781e4ebA804CE9a9803C67d0893436bB27D",  # renBTC
    "0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272",  # xSUSHI
    "0x6B3595068778DD592e39A122f4f5a5cF09C90fE2",  # SUSHI token
]

# ── Verified BSC legitimate contracts ───────────────────────────────────────
LEGIT_BSC_ADDRESSES = [
    "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82",  # CAKE (PancakeSwap)
    "0x10ED43C718714eb63d5aA57B78B54704E256024E",  # PancakeSwap Router
    "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73",  # PancakeSwap Factory
    "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",  # WBNB
    "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",  # USDC (BSC)
    "0x55d398326f99059fF775485246999027B3197955",  # USDT (BSC)
]


def get_all_legit_addresses():
    """Return combined list with chain labels."""
    result = [{"address": a, "chain": "ETH"} for a in LEGIT_ADDRESSES]
    result += [{"address": a, "chain": "BSC"} for a in LEGIT_BSC_ADDRESSES]
    # Deduplicate
    seen = set()
    deduped = []
    for item in result:
        if item["address"].lower() not in seen:
            seen.add(item["address"].lower())
            deduped.append(item)
    return deduped


if __name__ == "__main__":
    addresses = get_all_legit_addresses()
    print(f"Total legitimate contracts: {len(addresses)}")
    eth = [a for a in addresses if a["chain"] == "ETH"]
    bsc = [a for a in addresses if a["chain"] == "BSC"]
    print(f"  ETH: {len(eth)}")
    print(f"  BSC: {len(bsc)}")
