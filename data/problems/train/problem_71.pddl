

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on-table b1)
(on b2 b4)
(on b3 b7)
(on-table b4)
(on b5 b3)
(on b6 b9)
(on b7 b2)
(on b8 b5)
(on b9 b8)
(clear b1)
(clear b6)
)
(:goal
(and
(on b3 b5)
(on b4 b3)
(on b5 b9)
(on b7 b6)
(on b8 b4)
(on b9 b7))
)
)


