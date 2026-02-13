import Sidebar from "@/components/Sidebar";

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="flex">
            <Sidebar />
            <main className="flex-1 min-h-screen bg-background relative overflow-y-auto custom-scrollbar">
                <div className="relative z-10 p-6 lg:p-10">
                    {children}
                </div>
            </main>
        </div>
    );
}
