(set-logic ALL)
; Constraint ID: a79016cdd8eb739a
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60163)) (False)
(assert (not (= x 60163)))

; Query: ((== x 60164)) (False)
(assert (not (not (= x 60164))))

(check-sat)
(get-model)
