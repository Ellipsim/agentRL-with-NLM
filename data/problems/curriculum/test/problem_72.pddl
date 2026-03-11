

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b7)
(on b2 b5)
(on b3 b8)
(on b4 b2)
(on b5 b6)
(on-table b6)
(on b7 b9)
(on b8 b4)
(on b9 b3)
(clear b1)
)
(:goal
(and
(on b2 b1)
(on b3 b2)
(on b4 b9)
(on b5 b6)
(on b6 b3)
(on b8 b5))
)
)


