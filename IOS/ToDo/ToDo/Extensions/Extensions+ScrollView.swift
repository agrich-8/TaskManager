import UIKit

extension UIScrollView {
    open override func addSubview(_ view: UIView) {
        view.translatesAutoresizingMaskIntoConstraints = false
        super.addSubview(view)
    }
}
