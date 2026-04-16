(set-logic ALL)
; Constraint ID: b40d0eb158b9b553
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60154)) (False)
(assert (not (= x 60154)))

; Query: ((== x 60155)) (False)
(assert (not (not (= x 60155))))

(check-sat)
(get-model)
