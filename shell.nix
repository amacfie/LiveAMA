{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = [
    (pkgs.python311.withPackages (ps: [
      ps.fastapi
      ps.uvicorn
    ]))
  ];
}

