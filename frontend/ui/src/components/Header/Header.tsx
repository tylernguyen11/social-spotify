import React from "react";
import { Link } from "react-router";
import './Header.css';

interface HeaderProps {
    username?: string | null;
}

const Header: React.FC<HeaderProps> = ({ username }) => {
    return (
        <header>
            <Link to="/">
                Home
            </Link>
            <div>
                {username ? (
                    <span>Welcome, {username}</span>
                ) : (
                    <Link to="/login">
                        Login
                    </Link>
                )}
            </div>
        </header>
    );
};

export default Header;