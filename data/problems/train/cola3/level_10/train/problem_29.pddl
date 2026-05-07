

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b4)
(on b4 b7)
(ontable b5)
(on b6 b10)
(on b7 b9)
(on b8 b3)
(ontable b9)
(on b10 b8)
(on b11 b5)
(ontable b12)
(clear b1)
(clear b2)
(clear b6)
(clear b11)
(clear b12)
)
(:goal
(and
(on b1 b6)
(on b2 b12)
(on b4 b9)
(on b7 b4)
(on b8 b11)
(on b9 b1)
(on b11 b10)
(on b12 b7))
)
)


