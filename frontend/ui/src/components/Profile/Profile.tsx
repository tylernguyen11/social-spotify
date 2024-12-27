import { useParams } from 'react-router';
import { useEffect, useState } from 'react';
import { ProfileProps } from '../../interfaces/app_interfaces';

function Profile() {
    const { username } = useParams();
    const [profile, setProfile] = useState<ProfileProps | null>(null);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/api/profile/${username}`);
                const data:ProfileProps = await response.json();

                if (response.ok) {
                    setProfile(data);
                } else {
                    console.error('Failed to fetch profile:', data);
                }
            } catch (error) {
                console.error('Error fetching profile:', error);
            }
        };

        fetchProfile();
    }, [username]);

    if (!profile) return <div>Loading...</div>;

    return (
        <div>
            <h1>{profile.username}'s Profile</h1>
            <p>Bio: {profile.bio}</p>
        </div>
    );
}

export default Profile;
