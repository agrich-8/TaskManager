import Foundation

final class RegisterRequest {
    
    func postRequest(parameters:[String:Any],url:URL,with completion: (Int?,String?) -> Void) {
        
        // declare the parameter as a dictionary that contains string as key and value combination. considering inputs are valid
        
        //let parameters: [String: Any] = ["id": 13, "name": "jack","password":"testPass","description":"testDescription"]
        
        // create the url with URL
        //let url = URL(string: Resources.Links.API)! // change server url accordingly
        
        // create the session object
        let session = URLSession.shared
        
        // now create the URLRequest object using the url object
        var request = URLRequest(url: url)
        request.httpMethod = "POST" //set http method as POST
        
        // add headers for the request
        request.addValue("application/json", forHTTPHeaderField: "Content-Type") // change as per server requirements
        request.addValue("application/json", forHTTPHeaderField: "Accept")
        
        do {
            // convert parameters to Data and assign dictionary to httpBody of request
            request.httpBody = try JSONSerialization.data(withJSONObject: parameters, options: .prettyPrinted)
        } catch let error {
            //print(error.localizedDescription)
             completion(nil,error.localizedDescription)
            return
        }
        
        var errorTaskText:String?
        var responseTaskCode:Int?
        
        // create dataTask using the session object to send data to the server
        let task = session.dataTask(with: request) { data, response, error in
            
            if let error = error {
                //print("Post Request Error: \(error.localizedDescription)")
                errorTaskText = "Post Request Error: \(error.localizedDescription)"
                return
            }
            
            // ensure there is valid response code returned from this HTTP response
            guard let httpResponse = response as? HTTPURLResponse,
                  (200...299).contains(httpResponse.statusCode)
            else {
                //print("Invalid Response received from the server")
                errorTaskText = "Invalid Response received from the server"
                return
            }
            responseTaskCode = httpResponse.statusCode
            
            // ensure there is data returned
            //        guard let responseData = data else {
            //          print("nil Data received from the server")
            //          return
            //        }
            //
            //        do {
            //          // create json object from data or use JSONDecoder to convert to Model stuct
            //          if let jsonResponse = try JSONSerialization.jsonObject(with: responseData, options: .mutableContainers) as? [String: Any] {
            //            print(jsonResponse)
            //            // handle json response
            //          } else {
            //            print("data maybe corrupted or in wrong format")
            //            throw URLError(.badServerResponse)
            //          }
            //        } catch let error {
            //          print(error.localizedDescription)
            //        }
        }
        // perform the task
        task.resume()
        completion(responseTaskCode,errorTaskText)
    }
}

