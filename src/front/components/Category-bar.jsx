import { Link } from "react-router-dom";


export const CategoryBar = () => {

    return (
        <ul class="nav nav-underline ms-5">
  <li class="nav-item">
    
    <a class="nav-link active " aria-current="page" href="#">All Categories</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="#">Cars</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="#">Home and Garden</a>
  </li>
   <li class="nav-item">
    <a class="nav-link" href="#">Sports</a>
  </li>
   <li class="nav-item">
    <a class="nav-link" href="#">Fashion and Accessories</a>
  </li>
   <li class="nav-item">
    <a class="nav-link" href="#">Technology and electronics</a>
  </li>

</ul>

    );
};