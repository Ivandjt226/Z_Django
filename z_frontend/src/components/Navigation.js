
import React from 'react';
import {
  CDBSidebar,
  CDBSidebarContent,
  CDBSidebarHeader,
  CDBSidebarMenu,
  CDBSidebarMenuItem,
} from 'cdbreact';

import {NavLink} from 'react-router-dom';
import {Navbar} from 'react-bootstrap';
//import logo from '../static/logo.png'
import logoEd from '../static/Bot_IA.png'
import "../App.css";


const Navigation = () => {
  return (
    <div>
    <Navbar bg="dark" variant="dark" expand="lg" id="my-nav">
        <Navbar.Brand className="app-logo" href="/">
            <img
              src={logoEd}
              width="40"
              height="50"
              className="d-inline-block align-center"
              alt="React Bootstrap logo"
              exact = "true"
            />{' '}
            <strong>Asistente Virtual Robótico: Edison Robot</strong>
        </Navbar.Brand>
    </Navbar>
    <div className='sidebar'>
    <CDBSidebar textColor="#333" backgroundColor="#f0f0f0">
        <CDBSidebarHeader prefix={<i className="fa fa-bars" />}>
          Ruta de Navegación
        </CDBSidebarHeader>
        <CDBSidebarContent>
          <CDBSidebarMenu>
            <NavLink exact="true" to="/">
              <CDBSidebarMenuItem icon="home">Home</CDBSidebarMenuItem>
            </NavLink>
            <NavLink to="/Elaine_Assistant">
              <CDBSidebarMenuItem icon="laptop">Conversación</CDBSidebarMenuItem>
            </NavLink>
            {/*<NavLink to="/Vision_camera">
              <CDBSidebarMenuItem icon="camera">Detección</CDBSidebarMenuItem>
            </NavLink>*/}
            <NavLink to="/ReadAPI">
              <CDBSidebarMenuItem icon="smile">Conexión API</CDBSidebarMenuItem>
            </NavLink>
            <NavLink exact="true" to="/List">
              <CDBSidebarMenuItem icon="list">Listar usuarios</CDBSidebarMenuItem>
            </NavLink>
            <NavLink to="/Manage">
              <CDBSidebarMenuItem icon="user">Administrar usuarios</CDBSidebarMenuItem>
            </NavLink>
            <NavLink to="/Metrics">
              <CDBSidebarMenuItem icon="tools">Metricas</CDBSidebarMenuItem>
            </NavLink>
          </CDBSidebarMenu>
        </CDBSidebarContent>
      </CDBSidebar>
    </div>
    </div>
    
  );
};

export default Navigation;