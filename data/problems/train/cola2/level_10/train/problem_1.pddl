

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(ontable b3)
(on b4 b3)
(on b5 b2)
(on b6 b4)
(on b7 b10)
(on b8 b7)
(ontable b9)
(ontable b10)
(on b11 b9)
(on b12 b8)
(clear b5)
(clear b6)
(clear b11)
(clear b12)
)
(:goal
(and
(on b1 b7)
(on b5 b2)
(on b6 b8)
(on b7 b12)
(on b8 b10)
(on b9 b6)
(on b10 b11)
(on b11 b3)
(on b12 b4))
)
)


