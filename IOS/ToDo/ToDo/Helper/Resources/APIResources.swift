import Foundation

protocol APIResource {
    associatedtype ModelType:Decodable
    var methodPath:String {get}
}

extension APIResource {
    var url:URL {
        return URL(string: Resources.Links.PostURL)!
    }
}
