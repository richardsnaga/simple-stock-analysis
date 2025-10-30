"use client";

import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  IconButton,
} from "@mui/material";
import { Home, Settings, Menu } from "@mui/icons-material";
import Link from "next/link";

interface SidebarProps {
  open: boolean;
  setOpen: (open: boolean) => void;
}

const drawerWidth = 240;

const Sidebar = ({ open, setOpen }: SidebarProps) => {
  return (
    <>
      <Drawer
        variant="persistent"
        open={open}
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
      >
        <Toolbar sx={{ justifyContent: "space-between", px: 2 }}>
          <Typography variant="h6">My App</Typography>
          <IconButton onClick={() => setOpen(false)}>
            <Menu />
          </IconButton>
        </Toolbar>
        <List>
          {[
            { text: "Dashboard", icon: <Home />, link: "/" },
            { text: "Settings", icon: <Settings />, link: "/apps/tes" },
          ].map((item) => (
            <ListItem key={item.text} disablePadding>
              <ListItemButton component={Link} href={item.link}>
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Drawer>

      {!open && (
        <IconButton
          onClick={() => setOpen(true)}
          sx={{ position: "fixed", top: 16, left: 16 }}
        >
          <Menu />
        </IconButton>
      )}
    </>
  );
};

export default Sidebar;
