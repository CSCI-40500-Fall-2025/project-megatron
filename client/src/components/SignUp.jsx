import React, { useState, useMemo } from "react";

export default function SignUp() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirm, setConfirm] = useState("");
    const [touched, setTouched] = useState({
        email: false,
        password: false,
        confirm: false,
    });
    const [submitting, setSubmitting] = useState(false);

    const emailIsValid = useMemo(() => /^\S+@\S+\.\S+$/.test(email), [email]);

    const passwordLengthValid = password.length >= 12;
    const passwordHasNumber = /\d/.test(password);
    const passwordHasSpecial = /[^A-Za-z0-9]/.test(password);
    const passwordIsValid = passwordLengthValid && passwordHasNumber && passwordHasSpecial;

    const passwordsMatch = password === confirm && confirm.length > 0;
    const canSubmit = emailIsValid && passwordIsValid && passwordsMatch && !submitting;

    function handleSubmit(e) {
        e.preventDefault();
        setTouched({ email: true, password: true, confirm: true });
        if (!canSubmit) return;

        setSubmitting(true);
        // demo submit - replace with real API call
        setTimeout(() => {
            console.log("Submitting", { email });
            setSubmitting(false);
            setEmail("");
            setPassword("");
            setConfirm("");
            setTouched({ email: false, password: false, confirm: false });
            alert("Sign up successful (demo)");
        }, 800);
    }

    function fieldError(show, message) {
        if (!show) return null;
        return <div>{message}</div>;
    }

    return (
        <div>
            <form onSubmit={handleSubmit} noValidate>
                <h2>Create account</h2>

                <label>
                    Email
                    <input
                        aria-label="email"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        onBlur={() => setTouched((t) => ({ ...t, email: true }))}
                        required
                    />
                </label>
                {fieldError(touched.email && !emailIsValid, "Enter a valid email address.")}

                <label>
                    Password
                    <input
                        aria-label="password"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        onBlur={() => setTouched((t) => ({ ...t, password: true }))}
                        required
                    />
                </label>

                <div>
                    <div>• At least 12 characters {passwordLengthValid ? "✓" : ""}</div>
                    <div>• At least one number {passwordHasNumber ? "✓" : ""}</div>
                    <div>• At least one special character {passwordHasSpecial ? "✓" : ""}</div>
                    {touched.password && !passwordIsValid && <div>Password does not meet requirements.</div>}
                </div>

                <label>
                    Confirm password
                    <input
                        aria-label="confirm-password"
                        type="password"
                        value={confirm}
                        onChange={(e) => setConfirm(e.target.value)}
                        onBlur={() => setTouched((t) => ({ ...t, confirm: true }))}
                        required
                    />
                </label>
                {fieldError(touched.confirm && !passwordsMatch, "Passwords do not match.")}

                <button type="submit" disabled={!canSubmit}>
                    {submitting ? "Creating…" : "Create account"}
                </button>
            </form>
        </div>
    );
}
