{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # generic
            ansible
            ansible-lint
            openssh
          ];
          EDITOR = "${pkgs.nano}/bin/nano";
          ANSIBLE_PRIVATE_KEY_FILE = "keys/ci_woodpecker-ci_org.id_ed25519";
          ANSIBLE_VAULT_PASSWORD_FILE = "vault-pass.secret";
        };
      }
    );
}
