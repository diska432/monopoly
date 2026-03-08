import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
import { Session, User } from "@supabase/supabase-js";
import { supabase } from "../lib/supabase";

interface AuthContextValue {
  user: User | null;
  session: Session | null;
  loading: boolean;
  displayName: string;
  signUp: (email: string, password: string, name: string) => Promise<string | null>;
  signIn: (email: string, password: string) => Promise<string | null>;
  signInWithGoogle: () => Promise<void>;
  signOut: () => Promise<void>;
  getAccessToken: () => Promise<string | null>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be inside AuthProvider");
  return ctx;
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [session, setSession] = useState<Session | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session: s } }) => {
      // #region agent log
      fetch('http://127.0.0.1:7566/ingest/8db1c7ed-c122-43c4-b932-92b1335506ed',{method:'POST',headers:{'Content-Type':'application/json','X-Debug-Session-Id':'b45bcf'},body:JSON.stringify({sessionId:'b45bcf',location:'useAuth.tsx:getSession',message:'Initial getSession result',data:{hasSession:!!s,hasUser:!!s?.user,email:s?.user?.email||null,tokenLen:s?.access_token?.length||0},timestamp:Date.now()})}).catch(()=>{});
      // #endregion
      setSession(s);
      setUser(s?.user ?? null);
      setLoading(false);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, s) => {
      // #region agent log
      fetch('http://127.0.0.1:7566/ingest/8db1c7ed-c122-43c4-b932-92b1335506ed',{method:'POST',headers:{'Content-Type':'application/json','X-Debug-Session-Id':'b45bcf'},body:JSON.stringify({sessionId:'b45bcf',location:'useAuth.tsx:onAuthStateChange',message:'Auth state changed',data:{event:_event,hasSession:!!s,hasUser:!!s?.user,email:s?.user?.email||null,tokenLen:s?.access_token?.length||0},timestamp:Date.now(),hypothesisId:'H2'})}).catch(()=>{});
      // #endregion
      setSession(s);
      setUser(s?.user ?? null);
      if (s) setLoading(false);
    });

    return () => subscription.unsubscribe();
  }, []);

  const signUp = useCallback(async (email: string, password: string, name: string): Promise<string | null> => {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: { data: { full_name: name } },
    });
    // #region agent log
    fetch('http://127.0.0.1:7566/ingest/8db1c7ed-c122-43c4-b932-92b1335506ed',{method:'POST',headers:{'Content-Type':'application/json','X-Debug-Session-Id':'b45bcf'},body:JSON.stringify({sessionId:'b45bcf',location:'useAuth.tsx:signUp',message:'signUp result',data:{hasUser:!!data?.user,hasSession:!!data?.session,userId:data?.user?.id||null,email:data?.user?.email||null,confirmed:data?.user?.email_confirmed_at||null,error:error?.message||null},timestamp:Date.now(),hypothesisId:'H2'})}).catch(()=>{});
    // #endregion
    if (error) return error.message;

    if (data.session) return null;

    const { error: signInErr } = await supabase.auth.signInWithPassword({ email, password });
    // #region agent log
    fetch('http://127.0.0.1:7566/ingest/8db1c7ed-c122-43c4-b932-92b1335506ed',{method:'POST',headers:{'Content-Type':'application/json','X-Debug-Session-Id':'b45bcf'},body:JSON.stringify({sessionId:'b45bcf',location:'useAuth.tsx:signUp.autoSignIn',message:'Auto sign-in after signUp',data:{error:signInErr?.message||null},timestamp:Date.now(),hypothesisId:'H2-fix'})}).catch(()=>{});
    // #endregion
    if (signInErr) return "NEEDS_CONFIRM";

    return null;
  }, []);

  const signIn = useCallback(async (email: string, password: string): Promise<string | null> => {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    // #region agent log
    fetch('http://127.0.0.1:7566/ingest/8db1c7ed-c122-43c4-b932-92b1335506ed',{method:'POST',headers:{'Content-Type':'application/json','X-Debug-Session-Id':'b45bcf'},body:JSON.stringify({sessionId:'b45bcf',location:'useAuth.tsx:signIn',message:'signIn result',data:{hasUser:!!data?.user,hasSession:!!data?.session,tokenLen:data?.session?.access_token?.length||0,error:error?.message||null},timestamp:Date.now(),hypothesisId:'H3'})}).catch(()=>{});
    // #endregion
    return error?.message ?? null;
  }, []);

  const signInWithGoogle = useCallback(async () => {
    await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: window.location.origin,
        queryParams: { prompt: "select_account" },
      },
    });
  }, []);

  const signOut = useCallback(async () => {
    await supabase.auth.signOut();
  }, []);

  const getAccessToken = useCallback(async (): Promise<string | null> => {
    const { data } = await supabase.auth.getSession();
    return data.session?.access_token ?? null;
  }, []);

  const displayName =
    user?.user_metadata?.full_name ||
    user?.user_metadata?.name ||
    user?.email?.split("@")[0] ||
    "Player";

  return (
    <AuthContext.Provider
      value={{ user, session, loading, displayName, signUp, signIn, signInWithGoogle, signOut, getAccessToken }}
    >
      {children}
    </AuthContext.Provider>
  );
};
