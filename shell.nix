{
  pkgs ?
    import (builtins.fetchTarball {
      url = "https://github.com/NixOS/nixpkgs/archive/950820435387e34beaf8fdc355602c8ae4d89823.tar.gz";
      sha256 = "sha256:0j22hm76r5z5z3nba5ar44cqi104zxc14hr0i9yhda3wfg17nhx1";
    }) {},
}:
pkgs.mkShell {
  packages = [
    (pkgs.python311.withPackages (ps: [
      ps.fastapi
      ps.uvicorn
    ]))
  ];
}

