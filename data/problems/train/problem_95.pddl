

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b10)
(ontable b3)
(on b4 b8)
(on b5 b3)
(on b6 b11)
(on b7 b1)
(ontable b8)
(ontable b9)
(on b10 b5)
(on b11 b9)
(clear b2)
(clear b4)
(clear b7)
)
(:goal
(and
(on b1 b9)
(on b2 b11)
(on b3 b5)
(on b4 b8)
(on b5 b10)
(on b7 b2)
(on b9 b4)
(on b10 b6))
)
)


