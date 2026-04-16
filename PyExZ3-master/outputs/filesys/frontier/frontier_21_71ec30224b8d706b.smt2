(set-logic ALL)
; Constraint ID: 71ec30224b8d706b
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60541)) (False)
(assert (not (= x 60541)))

; Query: ((== x 60542)) (False)
(assert (not (not (= x 60542))))

(check-sat)
(get-model)
