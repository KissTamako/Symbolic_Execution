(set-logic ALL)
; Frontier Constraint ID: 63eaca34c6120de7
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1336)) (False)
(assert (not (= x 1336)))

; Query: ((== x 1337)) (False)
(assert (not (not (= x 1337))))

(check-sat)
(get-model)
