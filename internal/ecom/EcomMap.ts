import AgesThreeAndUpCa from "./AgesThreeAndUp"
import ArgamahobbyCom from "./ArgamahobbyCom"
import GundamhangarCom from "./GundamhangarCom"
import GundamhobbyCa from "./GundamhobbyCa"
import NiigsCa from "./NiigsCa"
// import ScifianimeCa from "./ScifianimeCa" Store is now closed :(
import AnimeExtreme from "./AnimeExtreme"
import Ecom from "./Ecom"
import EcomConfig from "./EcomConfig"

const map: { [key: string]: new (config: EcomConfig) => Ecom } = {
    "https://animextreme.ca": AnimeExtreme,
    "https://server.gundamhangar.com": GundamhangarCom,
    "https://niigs.ca": NiigsCa,
    "https://www.gundamhobby.ca": GundamhobbyCa,
    "https://www.agesthreeandup.ca": AgesThreeAndUpCa,
    "https://argamahobby.com": ArgamahobbyCom,
}
export default map
