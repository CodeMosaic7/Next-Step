import {Routes,Route} from 'react-router-dom';

import Home from "./pages/Home";
import Login from "./pages/Login";
import Assessment from "./pages/Assessment";
import CareerDashboard from "./pages/CareerDashboard";
const App=()=>{
  return(
    <Routes>

   <Route path="/" element={<Home/>}/>
   <Route path="/login" element={<Login/>}/>
   <Route path="/assessment" element={<Assessment/>}/>
   <Route path="/career-dashboard" element={<CareerDashboard/>}/>
   </Routes>
  )
}


export default App;