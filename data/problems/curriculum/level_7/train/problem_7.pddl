

(define (problem BW-rand-8)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 )
(:init
(arm-empty)
(on b1 b5)
(on b2 b6)
(on b3 b7)
(on-table b4)
(on b5 b2)
(on b6 b3)
(on-table b7)
(on b8 b1)
(clear b4)
(clear b8)
)
(:goal
(and
(on b1 b7)
(on b2 b8)
(on b3 b1)
(on b5 b6)
(on b8 b4))
)
)


