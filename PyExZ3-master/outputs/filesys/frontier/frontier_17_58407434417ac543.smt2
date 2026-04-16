(set-logic ALL)
; Frontier Constraint ID: 58407434417ac543
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1636)) (False)
(assert (not (= x 1636)))

; Query: ((== x 1637)) (False)
(assert (not (not (= x 1637))))

(check-sat)
(get-model)
