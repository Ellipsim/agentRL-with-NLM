

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b7)
(ontable b3)
(on b4 b10)
(ontable b5)
(on b6 b4)
(on b7 b6)
(on b8 b9)
(ontable b9)
(on b10 b1)
(on b11 b5)
(clear b2)
(clear b3)
(clear b11)
)
(:goal
(and
(on b1 b3)
(on b2 b9)
(on b3 b8)
(on b4 b6)
(on b5 b1)
(on b8 b11)
(on b9 b10)
(on b11 b4))
)
)


