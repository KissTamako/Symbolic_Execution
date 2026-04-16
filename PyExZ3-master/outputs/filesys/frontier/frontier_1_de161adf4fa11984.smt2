(set-logic ALL)
; Frontier Constraint ID: de161adf4fa11984
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1462)) (False)
(assert (not (= x 1462)))

; Query: ((== x 1463)) (False)
(assert (not (not (= x 1463))))

(check-sat)
(get-model)
