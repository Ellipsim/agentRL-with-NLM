

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b2)
(on-table b2)
(on b3 b9)
(on b4 b3)
(on-table b5)
(on b6 b4)
(on b7 b1)
(on-table b8)
(on b9 b10)
(on-table b10)
(clear b5)
(clear b6)
(clear b7)
(clear b8)
)
(:goal
(and
(on b1 b4)
(on b4 b5)
(on b5 b8)
(on b7 b6)
(on b8 b9)
(on b9 b10))
)
)


