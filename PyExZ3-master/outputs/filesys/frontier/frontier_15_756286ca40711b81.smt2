(set-logic ALL)
; Frontier Constraint ID: 756286ca40711b81
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1858)) (False)
(assert (not (= x 1858)))

; Query: ((== x 1859)) (False)
(assert (not (not (= x 1859))))

(check-sat)
(get-model)
