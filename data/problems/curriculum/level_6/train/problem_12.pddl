

(define (problem BW-rand-7)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 )
(:init
(arm-empty)
(on b1 b2)
(on b2 b6)
(on-table b3)
(on b4 b3)
(on b5 b1)
(on-table b6)
(on b7 b5)
(clear b4)
(clear b7)
)
(:goal
(and
(on b2 b4)
(on b4 b5)
(on b5 b7)
(on b7 b3))
)
)


