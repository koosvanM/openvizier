import { useEffect, lazy, Suspense } from "react";
import { Switch, Route, Router, useLocation } from "wouter";
import { useHashLocation } from "wouter/use-hash-location";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/not-found";

// Route-splitting: alle pagina's lazy laden, inclusief PersonaFlow.
// Dit haalt de ~575 KB persona-JSON + cascade-engine uit de initial bundle.
const PersonaFlow = lazy(() => import("@/pages/PersonaFlow"));
const Hoofdpagina = lazy(() => import("@/pages/Hoofdpagina"));
const Methodologie = lazy(() => import("@/pages/Methodologie"));

function ScrollToTop() {
  const [location] = useLocation();
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "auto" });
  }, [location]);
  return null;
}

function AppRouter() {
  return (
    <>
      <ScrollToTop />
      <Suspense fallback={
        <div className="min-h-screen flex items-center justify-center bg-slate-50">
          <div className="flex flex-col items-center gap-3">
            <div className="w-10 h-10 border-3 border-sky-300 border-t-sky-600 rounded-full animate-spin" style={{ borderWidth: 3 }} />
            <div className="text-sm text-slate-500 font-medium">Gevolgenkaart laden…</div>
          </div>
        </div>
      }>
        <Switch>
          <Route path="/methodologie" component={Methodologie} />
          <Route path="/matrix" component={Hoofdpagina} />
          <Route path="/matrix/:rest*" component={Hoofdpagina} />
          <Route path="/" component={PersonaFlow} />
          <Route path="/:rest*" component={PersonaFlow} />
          <Route component={NotFound} />
        </Switch>
      </Suspense>
    </>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Router hook={useHashLocation}>
          <AppRouter />
        </Router>
      </TooltipProvider>
    </QueryClientProvider>
  );
}

export default App;
