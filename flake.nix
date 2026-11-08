{
  description = "Tlamina: a retro space shooter made with pygame-ce";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in
    {
      devShells = forAllSystems (pkgs:
        let
          pythonPackages = pkgs.python3.pkgs;
        in
        {
          default = pkgs.mkShell {
            packages = [
              (pkgs.python3.withPackages (ps: [ ps.pygame-ce ps.pytest ]))
              pkgs.ruff
              pkgs.gh
            ];

            shellHook = ''
              echo "🛸 Tlamina dev shell"
              echo "  🐍 Python     ${pkgs.python3.version}"
              echo "  🎮 pygame-ce  ${pythonPackages.pygame-ce.version}"
              echo "  🧪 pytest     ${pythonPackages.pytest.version}"
              echo "  🧹 ruff       ${pkgs.ruff.version}"
              echo "  🐙 gh         ${pkgs.gh.version}"
            '';
          };
        });
    };
}
