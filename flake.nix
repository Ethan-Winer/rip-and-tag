{
  description = "Nix flake for Rip and Tag";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";
  };

  outputs = { self , nixpkgs ,... }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
  in {
    devShells."${system}".default = pkgs.mkShell {
      packages = with pkgs; [
        python313
        python313Packages.yt-dlp
        python313Packages.musicbrainzngs
        python313Packages.youtube-search-python
        python313Packages.mutagen
        ffmpeg_7-headless
      ];

      shellHook = ''
        code .
        fish
      '';
    };
  };
}
