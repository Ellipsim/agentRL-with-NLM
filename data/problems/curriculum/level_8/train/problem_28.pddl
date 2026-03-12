

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b5)
(on b2 b10)
(on b3 b6)
(on b4 b1)
(on-table b5)
(on-table b6)
(on-table b7)
(on b8 b4)
(on-table b9)
(on b10 b8)
(clear b2)
(clear b3)
(clear b7)
(clear b9)
)
(:goal
(and
(on b3 b7)
(on b4 b3)
(on b5 b1)
(on b7 b2)
(on b9 b4)
(on b10 b9))
)
)


