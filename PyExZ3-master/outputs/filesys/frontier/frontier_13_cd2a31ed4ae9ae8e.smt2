(set-logic ALL)
; Constraint ID: cd2a31ed4ae9ae8e
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60379)) (False)
(assert (not (= x 60379)))

; Query: ((== x 60380)) (False)
(assert (not (not (= x 60380))))

(check-sat)
(get-model)
