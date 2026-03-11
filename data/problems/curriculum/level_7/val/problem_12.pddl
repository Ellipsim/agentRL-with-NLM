

(define (problem BW-rand-8)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 )
(:init
(arm-empty)
(on b1 b3)
(on b2 b4)
(on b3 b5)
(on-table b4)
(on b5 b8)
(on b6 b2)
(on b7 b6)
(on-table b8)
(clear b1)
(clear b7)
)
(:goal
(and
(on b2 b8)
(on b4 b6)
(on b5 b1)
(on b6 b5)
(on b7 b4))
)
)


