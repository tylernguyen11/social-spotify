export interface ProfileProps {
    username: string;
    display_name: string;
    profile_picture: string;
    bio: string;
    followers: number;
    following: number;
}

export interface SpotifyProps {
    id: number;
    name: string;
    image_url: string | null;
    spotify_url: string;
}

export interface ArtistProps extends SpotifyProps {
    followers: number;
    genres: string[];
}
